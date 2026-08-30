const FIELD_ORDER = [
  'Название компании','Страна / основной рынок','Сайт','Контактное лицо','Должность','E-mail','Телефон / мессенджер',
  'Ключевые направления деятельности','Основные продукты / услуги / технологии','Отрасль',
  'Международный опыт','Интересующие рынки','Опыт на целевом рынке',
  'Направления сотрудничества','Стадия задачи','Бюджет','Ориентировочный бюджет',
  'Ожидаемая поддержка','Успешный результат','Срок начала','Документы / сертификаты','Готовность предоставить дополнительную информацию'
];

function doGet() {
  return ContentService.createTextOutput('GO BIG form endpoint is active');
}

function doPost(e) {
  try {
    const payload = parsePayload_(e);
    if (!payload || Object.keys(payload).length === 0) throw new Error('Empty payload');
    if (String(payload.website2 || '').trim()) return json_({ok:true}); // honeypot

    const props = PropertiesService.getScriptProperties();
    const emailTo = props.getProperty('EMAIL_TO') || 'companygobig@gmail.com';
    const botToken = props.getProperty('TELEGRAM_BOT_TOKEN');
    const chatId = props.getProperty('TELEGRAM_CHAT_ID');

    const company = clean_(payload['Название компании'] || payload.company || 'Компания');
    const email = clean_(payload['E-mail'] || payload.email || '');
    const subject = 'Новая заявка GO BIG — ' + company;
    const text = buildText_(payload);
    const html = buildHtml_(payload);

    if (emailTo) {
      MailApp.sendEmail({
        to: emailTo,
        subject: subject,
        body: text,
        htmlBody: html,
        replyTo: email || undefined,
        name: 'GO BIG Website'
      });
    }

    if (botToken && chatId) {
      const telegramText = buildTelegram_(payload);
      UrlFetchApp.fetch('https://api.telegram.org/bot' + botToken + '/sendMessage', {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify({
          chat_id: chatId,
          text: telegramText,
          parse_mode: 'HTML',
          disable_web_page_preview: true
        }),
        muteHttpExceptions: true
      });
    }

    saveToSheet_(payload, props);
    return json_({ok:true});
  } catch (err) {
    console.error(err);
    return json_({ok:false,error:String(err && err.message ? err.message : err)});
  }
}

function parsePayload_(e) {
  if (!e) return {};
  if (e.postData && e.postData.contents) {
    const raw = e.postData.contents;
    try { return JSON.parse(raw); } catch (_) {}
  }
  return e.parameter || {};
}

function clean_(value) {
  if (Array.isArray(value)) return value.map(clean_).join(', ');
  return String(value == null ? '' : value).trim();
}

function fieldEntries_(payload) {
  const seen = {};
  const rows = [];
  FIELD_ORDER.forEach(key => {
    if (Object.prototype.hasOwnProperty.call(payload, key)) {
      const value = clean_(payload[key]);
      if (value) rows.push([key, value]);
      seen[key] = true;
    }
  });
  Object.keys(payload).forEach(key => {
    if (seen[key] || key === 'website2' || key === 'source') return;
    const value = clean_(payload[key]);
    if (value) rows.push([key, value]);
  });
  return rows;
}

function buildText_(payload) {
  const lines = ['Новая заявка с сайта GO BIG', ''];
  fieldEntries_(payload).forEach(row => lines.push(row[0] + ': ' + row[1]));
  lines.push('', 'Источник: ' + clean_(payload.source || 'gobigeurope.com'));
  lines.push('Дата: ' + Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'Europe/Belgrade', 'dd.MM.yyyy HH:mm'));
  return lines.join('\n');
}

function buildHtml_(payload) {
  const rows = fieldEntries_(payload).map(row =>
    '<tr><td style="padding:8px 12px;border-bottom:1px solid #e7eaed;color:#637080;vertical-align:top;width:34%">' + esc_(row[0]) + '</td>' +
    '<td style="padding:8px 12px;border-bottom:1px solid #e7eaed;color:#1f2a3d;vertical-align:top">' + esc_(row[1]).replace(/\n/g,'<br>') + '</td></tr>'
  ).join('');
  return '<div style="font-family:Arial,sans-serif;max-width:760px">' +
    '<h2 style="color:#0B6B45">Новая заявка GO BIG</h2>' +
    '<table style="width:100%;border-collapse:collapse">' + rows + '</table>' +
    '<p style="margin-top:18px;color:#7a8591;font-size:12px">Источник: ' + esc_(clean_(payload.source || 'gobigeurope.com')) + '</p>' +
    '</div>';
}

function buildTelegram_(payload) {
  const company = esc_(clean_(payload['Название компании'] || payload.company || 'Компания'));
  const contact = esc_(clean_(payload['Контактное лицо'] || ''));
  const email = esc_(clean_(payload['E-mail'] || payload.email || ''));
  const markets = esc_(clean_(payload['Интересующие рынки'] || ''));
  const task = esc_(clean_(payload['Направления сотрудничества'] || payload['Ожидаемая поддержка'] || ''));
  const parts = ['<b>Новая заявка GO BIG</b>', '', '<b>Компания:</b> ' + company];
  if (contact) parts.push('<b>Контакт:</b> ' + contact);
  if (email) parts.push('<b>E-mail:</b> ' + email);
  if (markets) parts.push('<b>Рынки:</b> ' + markets);
  if (task) parts.push('<b>Задача:</b> ' + task);
  return parts.join('\n').slice(0, 3900);
}

function saveToSheet_(payload, props) {
  const sheetId = props.getProperty('SHEET_ID');
  if (!sheetId) return;
  const sheetName = props.getProperty('SHEET_NAME') || 'Leads';
  const ss = SpreadsheetApp.openById(sheetId);
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) sheet = ss.insertSheet(sheetName);

  const entries = fieldEntries_(payload);
  const headers = ['Дата'].concat(entries.map(row => row[0]));
  if (sheet.getLastRow() === 0) sheet.appendRow(headers);
  sheet.appendRow([new Date()].concat(entries.map(row => row[1])));
}

function esc_(value) {
  return String(value || '')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;')
    .replace(/'/g,'&#39;');
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

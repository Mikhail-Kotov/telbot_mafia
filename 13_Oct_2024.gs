function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var range = e.range;
  var columnToUpdate = 10; // Последний столбец в строке - J
  var currentRow = range.getRow()

  // Проверяем, что название листа начинается с "MEL " и редактируемая ячейка находится в столбце J и не является заголовком
  if (sheet.getName().startsWith("MEL") && range.getColumn() != columnToUpdate && currentRow > 1) {
    var cell = sheet.getRange(currentRow, columnToUpdate);
    cell.setValue(new Date());
  }
}

function linkURL(reference) {
  var sheet = SpreadsheetApp.getActiveSheet();
  var formula = SpreadsheetApp.getActiveRange().getFormula();
  var args = formula.match(/=\w+\((.*)\)/i);
  try {
    var range = sheet.getRange(args[1]);
  }
  catch(e) {
    throw new Error(args[1] + ' is not a valid range');
  }
  
  var formulas = range.getRichTextValues();
  var output = [];
  for (var i = 0; i < formulas.length; i++) {
    var row = [];
    for (var j = 0; j < formulas[0].length; j++) {
      row.push(formulas[i][j].getLinkUrl());
    }
    output.push(row);
  }
  return output
}

function telHyperlink(cell) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('users');
  var data = sheet.getRange('A:A').getValues();
  var searchValue = cell;
  var rowIndex = -1;

  for (var i = 0; i < data.length; i++) {
    if (data[i][0] == searchValue) {
      rowIndex = i + 1; // +1 because getRange is 1-based
      break;
    }
  }

  if (rowIndex != -1) {
    var username = sheet.getRange('E' + rowIndex).getValue();
    var displayName = sheet.getRange('A' + rowIndex).getValue();
    var hyperlink = "https://t.me/" + username;
    Logger.log('HYPERLINK: ' + hyperlink + ', DISPLAY NAME: ' + displayName);
    var activeCell = SpreadsheetApp.getActiveSpreadsheet().getActiveCell();
    activeCell.setFormula('=HYPERLINK("' + hyperlink + '", "' + displayName + '")');
    return hyperlink
  } else {
    Logger.log('Value not found');
  }
}

function copyHyperlink(sourceRange, targetRange) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var sourceCell = sheet.getRange(sourceRange);
  var targetCell = sheet.getRange(targetRange);
  
  var hyperlink = sourceCell.getRichTextValue().getLinkUrl();
  var targetText = targetCell.getValue();
  
  var richText = SpreadsheetApp.newRichTextValue()
    .setText(targetText)
    .setLinkUrl(hyperlink)
    .build();
  
  targetCell.setRichTextValue(richText);
}

function getNextFiveSundays() {
  var today = new Date();
  var sundays = [];
  var dayOfWeek = today.getDay();
  var daysUntilSunday = (7 - dayOfWeek) % 7;

  for (var i = 0; i < 5; i++) {
    var nextSunday = new Date(today);
    nextSunday.setDate(today.getDate() + daysUntilSunday + (i * 7));
    var day = nextSunday.getDate();
    var month = nextSunday.getMonth() + 1; // Месяцы в JS начинаются с 0
    sundays.push(day + '/' + month);
  }
  // Logger.log(sundays);
  return sundays;
}

function duplicateSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var curr_city = "MEL"
  var sheet = spreadsheet.getSheetByName(curr_city);
  if (sheet) {
      var sundays = getNextFiveSundays();
  
    for (var i = 0; i < sundays.length; i++) {
      var calSheetName = curr_city + " " + sundays[i];
      var calSheet = spreadsheet.getSheetByName(calSheetName);
      if (calSheet == null) {
        var newSheet = sheet.copyTo(spreadsheet);
        newSheet.setName(calSheetName);
        newSheet.showSheet();
        Logger.log('Sheet "' + calSheetName + '" duplicated.');
      } else {
        Logger.log('Sheet "' + calSheetName + '" already exists.');
      }
    }
    SpreadsheetApp.flush();
  } else {
    Logger.log("Sheet not found");
  }
}

function onFormSubmit(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var lastRow = sheet.getLastRow();
  var newRow = lastRow + 1;
  var formData = e.values;
  
  for (var i = 0; i < formData.length; i++) {
    sheet.getRange(newRow, i + 1).setValue(formData[i]);
  }
}

function createTrigger() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  ScriptApp.newTrigger('onFormSubmit')
           .forSpreadsheet(sheet)
           .onFormSubmit()
           .create();
}

$(document).ready(function() {
  $('.score-form input').on('input', function() {
    let scoreField = $(this);
    let score = parseFloat(scoreField.val());
    let minScore = parseFloat(scoreField.attr('min'));
    let maxScore = parseFloat(scoreField.attr('max'));
    if (score < minScore || score > maxScore || isNaN(score) || !Number.isInteger(score)) {
      scoreField.css('background-color', '#f5c2c7');
    } else {
      scoreField.css('background-color', '');
    }
  });
});
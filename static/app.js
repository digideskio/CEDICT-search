(function() {
  var QUERY_WATCHER_POLL, SICK_POLL, last_q, normalize, query_watcher, results_tmpl, search, sickify_sick_inputs, time;

  SICK_POLL = 100;

  QUERY_WATCHER_POLL = 500;

  normalize = function(q) {
    return q.toLowerCase().replace(/[ ]+/g, ' ').trim();
  };

  last_q = '';

  time = function() {
    return (new Date).getTime();
  };

  results_tmpl = '\
<h1>{{search_type}} search: {{count}} results</h1>\
{{#results}}\
<div class="result">\
  <div class="hanzi">{{simplified}} / {{traditional}}</div>\
  <div class="pinyin">{{pinyin}}</div>\
  <ol>\
  {{#english_list}}\
    <li>{{.}}</li>\
  {{/english_list}}\
  </ol>\
</div>\
{{/results}}\
';

  search = function(q) {
    var start, url;
    if (q && q !== last_q) {
      start = time();
      last_q = q;
      $('.sick-input').addClass('searching');
      url = '/search/' + encodeURIComponent(q);
      return $.getJSON(url, function(json) {
        var end, rendered;
        if (q === last_q) {
          rendered = Mustache.render(results_tmpl, json);
          $('#results').html(rendered);
          $('.sick-input').removeClass('searching');
          end = time();
          return console.log(end - start);
        }
      });
    }
  };

  sickify_sick_inputs = function() {
    return $('.sick-input').each(function() {
      var div, input, sick_input_watcher;
      div = $(this);
      input = div.find('input');
      input.focus(function() {
        return div.addClass('focused');
      });
      input.blur(function() {
        return div.removeClass('focused');
      });
      sick_input_watcher = function() {
        return div.toggleClass('populated', input.val().trim() !== '');
      };
      return setInterval(sick_input_watcher, SICK_POLL);
    });
  };

  query_watcher = function() {
    var q;
    q = normalize($('#search-bar').val());
    return search(q);
  };

  $(function() {
    $('.sick-input input').focus();
    sickify_sick_inputs();
    return setInterval(query_watcher, QUERY_WATCHER_POLL);
  });

}).call(this);

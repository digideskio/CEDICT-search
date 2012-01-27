
SICK_POLL = 100
QUERY_WATCHER_POLL = 500

normalize = (q) -> q.toLowerCase().replace(/[ ]+/g, ' ').trim()

last_q = ''

time = -> (new Date).getTime()

results_tmpl = '
<h1>{{search_type}} search: {{count}} results</h1>
{{#results}}
<div class="result">
  <div class="hanzi">{{simplified}} / {{traditional}}</div>
  <div class="pinyin">{{pinyin}}</div>
  <ol>
  {{#english_list}}
    <li>{{.}}</li>
  {{/english_list}}
  </ol>
</div>
{{/results}}
'

search = (q) ->
  if q and q != last_q
    start = time()
    last_q = q
    $('.sick-input').addClass 'searching'
    url = '/search/' + encodeURIComponent(q)
    $.getJSON url, (json) ->
      unless q != last_q # ajax: these could come back in any order
        rendered = Mustache.render(results_tmpl, json)
        $('#results').html(rendered)
        $('.sick-input').removeClass 'searching'
        end = time()
        console.log end - start

sickify_sick_inputs = ->
  $('.sick-input').each ->
    div = $(this)
    input = div.find 'input'
    input.focus ->
      div.addClass 'focused'
    input.blur ->
      div.removeClass 'focused'

    sick_input_watcher = ->
      div.toggleClass 'populated', input.val().trim() != ''

    setInterval sick_input_watcher, SICK_POLL

query_watcher = ->
  q = normalize $('#search-bar').val()
  search q

$ ->
  $('.sick-input input').focus()
  sickify_sick_inputs()
  setInterval(query_watcher, QUERY_WATCHER_POLL)

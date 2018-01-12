
Vue.component('lepv-chart-card', {

  delimiters: ['[[',']]'],

  props: [
    'chart_id',
    'header',
    'icon'
  ],

  template: `

  <div class="col-md-12">
    <div :id='[[chart_id]]' class="card mb-3">
        <div class="card-header">
            <i :class="[[icon]]"></i> [[header]]
        </div>
        <div class="card-body"><div class="chart-panel"></div></div>
        <div class="card-footer small text-muted" hidden><i class="fa fa-bell" aria-hidden="true"> </i></div>
    </div>
  </div>

  `
})

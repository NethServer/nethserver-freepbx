<template>
  <div>
    <h1>{{$t('dashboard.title')}}</h1>

    <div class="blank-slate-pf">
      <div class="blank-slate-pf-icon">
        <span class="fa fa-phone-square phone-icon"></span>
      </div>
      <h1>
        {{$t('dashboard.freepbx_admin_dashboard')}}
      </h1>
      <p>
        {{$t('dashboard.freepbx_description')}}
      </p>
      <div class="blank-slate-pf-main-action">
        <a 
          :href="freePbxUrl"
          target="_blank"
          class="btn btn-primary btn-lg">{{$t('dashboard.open_dashboard')}}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  components: {
  },
  props: {
  },
  mounted() {
  },
  data() {
    return {
      freePbxUrl: window.location.protocol + '//' + window.location.hostname + '/freepbx'
    }
  }
}
</script>

<style>
.empty-phone {
  margin: 2em;
  text-align: center;
  color: #9c9c9c;
}

.empty-phone .fa {
  font-size: 200px;
  color: #bbbbbb;
}

.center {
  text-align: center;
}

.phone-icon {
  font-size: 57.6px;
}
</style>
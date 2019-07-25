<template>
  <div>
    <h1 class="app-title">{{$t('settings.title')}}</h1>

    <h3 class="app-subtitle mt-20">External access</h3>
    <div class="row">
      <div class="col-lg-12">
        <div class="col-md-6">
          <form class="form-horizontal">
            <div class="form-group">
              <label class="col-sm-5 control-label" for="textInput-markup">Allow external IAX access</label>
              <div class="col-sm-7">
                <input class="bootstrap-switch" id="bootstrap-switch-state" type="checkbox" checked>
              </div>
            </div>
            <div class="form-group">
              <label class="col-sm-5 control-label" for="textInputDisabled-markup">Allow external SIP TLS access</label>
              <div class="col-sm-7">
                <input class="bootstrap-switch" id="bootstrap-switch-state" type="checkbox" checked>
              </div>
            </div>
            <div class="form-group has-error">
              <label class="col-sm-5 control-label" for="inputError-markup">Allow external WebRTC and WebSocket
                access</label>
              <div class="col-sm-7">
                <input class="bootstrap-switch" id="bootstrap-switch-state" type="checkbox" checked>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>

    <h3 class="app-subtitle mt-20">Web interface access</h3>
    <div class="row">
      <div class="col-lg-12">
        <p>
          <button class="btn btn-primary btn-lg" type="button">Create new</button>
        </p>
        <div class="inbound-margin-top">
          <div class="list-group list-view-pf list-view-pf-view list-header">
            <div class="list-group-item list-item-header">
              <div class="list-view-pf-actions w-74">
                <label class="ml-10">Actions</label>
              </div>
              <div class="list-view-pf-main-info">
                <div class="w-50 list-view-pf-left">
                </div>
                <div class="list-view-pf-body">
                  <div class="list-view-pf-additional-info">
                    <div class="list-view-pf-additional-info-item">
                      <label>Nethwork</label>
                    </div>
                  </div>
                  <div class="list-view-pf-additional-info">
                    <div class="list-view-pf-additional-info-item">
                      <label>Nethwork mask</label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="list-group-item">
              <div class="list-view-pf-actions"><button class="btn btn-default"><span
                    class="fa fa-times span-right-margin"></span>
                  Delete
                </button>

              </div>
              <div class="list-view-pf-main-info">
                <div class="list-view-pf-left disabled"><span class="fa fa-sitemap list-view-pf-icon-sm"></span></div>
                <div class="list-view-pf-body">
                  <div class="list-view-pf-additional-info">
                    <div class="list-view-pf-additional-info-item">
                      <span>192.168.5.81</span>
                    </div>
                  </div>
                  <div class="list-view-pf-additional-info">
                    <div class="list-view-pf-additional-info-item">
                      <span>255.255.255.0</span>
                    </div>
                  </div>
                  <div class="list-view-pf-additional-info"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Settings",
    components: {

    },
    props: {

    },
    mounted() {
      $(".bootstrap-switch").ready(function () {
        $(".bootstrap-switch").bootstrapSwitch();
      });
    },
    data() {
      return {
        testValue: false
      };
    },
  }
</script>

<style>
  .mt-20 {
    margin-top: 20px;
  }
  .ml-10 {
    margin-left: 10px;
  }
  .w-50 {
    width: 50px !important;
  }
  .w-105 {
    width: 105px !important;
  }
  .w-89 {
    width: 89px !important;
  }
  .w-74 {
    width: 74px !important;
  }

  .app-title {
    margin-bottom: 35px !important;
    padding-bottom: 17px !important;
    border-bottom: 1px solid #D5D5D5 !important;
  }

  .app-subtitle {
    margin-bottom: 27px !important;
    font-weight: 500 !important;
    font-size: 18px !important;
  }

</style>
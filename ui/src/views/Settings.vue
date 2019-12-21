<template>
  <div>
    <h2>{{$t('settings.title')}}</h2>

    <!-- error message -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissable">
      <button type="button" class="close" @click="closeErrorMessage()" aria-label="Close">
        <span class="pficon pficon-close"></span>
      </button>
      <span class="pficon pficon-error-circle-o"></span>
      {{ errorMessage }}.
    </div>

    <!-- modal for adding a web interface access -->
    <div class="modal fade" id="modalNewWebInterfaceAccess" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
              <span class="pficon pficon-close"></span>
            </button>
            <h4 class="modal-title">{{$t('settings.add_web_interface_access')}}</h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="createNewWebInterfaceAccess">
            <div class="modal-body">
              <div class="form-group" v-bind:class="{ 'has-error': showErrorIpAddress }">
                <label class="col-sm-3 control-label" for="txIpAddressCreate">{{$t('settings.ip_address')}}</label>
                <div class="col-sm-9">
                  <input type="text" id="txIpAddressCreate" v-model="ipAddressCreate" class="form-control">
                  <span class="help-block" v-if="showErrorIpAddress">{{$t('settings.ipAddress_validation')}}</span>
                </div>
              </div>
              <div class="form-group" v-bind:class="{ 'has-error': showErrorNetmask }">
                <label class="col-sm-3 control-label" for="txNetmaskCreate">{{$t('settings.netmask')}}</label>
                <div class="col-sm-9">
                  <input type="text" id="txNetmaskCreate" v-model="netmaskCreate" class="form-control">
                  <span class="help-block" v-if="showErrorNetmask">{{$t('settings.netmask_validation')}}</span>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">{{$t('cancel')}}</button>
              <button type="submit" class="btn btn-primary">
                {{$t('create')}}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- modal to confirm web interface access deletion -->
    <div class="modal fade" id="modalDeleteWebInterfaceAccess" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
              <span class="pficon pficon-close"></span>
            </button>
            <h4 class="modal-title" id="modalUserDeleteLabel">
              {{$t('settings.delete_web_interface_access')}} ({{ accessToDeleteIpAddress }} - {{ accessToDeleteNetmask }})
            </h4>
          </div>
          <form class="form-horizontal" v-on:submit.prevent="deleteAccess">
            <div class="modal-body">
              <div class="alert alert-warning alert-dismissable">
                <span class="pficon pficon-warning-triangle-o"></span>
                <strong>{{$t('warning')}}!</strong>
                <span class="margin-left-5">
                  {{$t('settings.delete_web_interface_access_message')}}.
                </span>
              </div>
              <form class="form-horizontal">
                <div class="form-group">
                  <label class="col-sm-3 control-label">
                    {{$t('settings.are_you_sure')}}?
                  </label>
                </div>
              </form>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">{{$t('cancel')}}</button>
              <button type="submit" class="btn btn-danger">
                {{$t('delete')}}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="!uiLoaded" class="spinner spinner-lg"></div>
    <div v-if="uiLoaded">
      <form class="form-horizontal" v-on:submit.prevent="btSaveClick">
        <h2>{{$t('settings.external_access')}}</h2>
        <div class="row">
          <div class="col-lg-12">
            <div class="col-md-6">
              <div class="form-group">
                <label class="col-sm-5 control-label">
                  {{$t('settings.allow_external_iax_access')}}
                  <doc-info
                    :placement="'top'"
                    :title="$t('settings.allow_external_iax_access')"
                    :chapter="'allow_external_iax_access'"
                    :inline="true"
                  ></doc-info>
                </label>
                <div class="col-sm-5">
                  <input
                    v-model="allowExternalIAX"
                    type="checkbox"
                    class="form-control"
                  >
                </div>
              </div>
              <div class="form-group">
                <label class="col-sm-5 control-label">
                  {{$t('settings.allow_external_sip_tls_access')}}
                  <doc-info
                    :placement="'top'"
                    :title="$t('settings.allow_external_sip_tls_access')"
                    :chapter="'allow_external_sip_tls_access'"
                    :inline="true"
                  ></doc-info>
                </label>
                <div class="col-sm-5">
                  <input
                    v-model="allowExternalSIPS"
                    type="checkbox"
                    class="form-control"
                  >
                </div>
              </div>

              <!-- save button -->
              <div class="form-group">
                <label class="col-sm-5 control-label">
                </label>
                <div class="col-sm-5">
                  <button 
                    class="btn btn-primary" 
                    type="submit"
                  >
                    {{$t('save')}}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
      <div class="divider"></div>

      <form class="form-horizontal">
        <h2>{{$t('settings.web_interface_access')}}</h2>
        <h3>{{$t('actions')}}</h3>
        <div class="row">
          <div class="col-lg-12">
            <p>
              <button 
                class="btn btn-primary btn-lg" 
                type="button"
                @click="showModalNewWebInterfaceAccess()"
                data-toggle="modal" data-target="#modalNewWebInterfaceAccess"
              >
                {{$t('settings.create_new_access')}}
              </button>
            </p>

            <!-- web interface access table -->
            <vue-good-table 
              v-if="validFromList.length > 0"
              :customRowsPerPageDropdown="[25,50,100]"
              :perPage="25"
              :columns="tableColumns"
              :rows="validFromList"
              :lineNumbers="false"
              :defaultSortBy="{field: 'ipAddress', type: 'asc'}"
              :globalSearch="true"
              :paginate="true"
              styleClass="table"
              :nextText="tableLangsTexts.nextText"
              :prevText="tableLangsTexts.prevText"
              :rowsPerPageText="tableLangsTexts.rowsPerPageText"
              :globalSearchPlaceholder="tableLangsTexts.globalSearchPlaceholder"
              :ofText="tableLangsTexts.ofText"
            >
              <template slot="table-row" slot-scope="props">
                <td class="fancy">
                    {{ props.row.ipAddress }}
                </td>
                <td class="fancy">
                  {{ props.row.netmask}}
                </td>
                <td class="fancy">
                  <button
                    type="button"
                    @click="requestDeleteAccess(props.row.ipAddress, props.row.netmask)"
                    class="btn btn-danger button-minimum"
                    data-toggle="modal" data-target="#modalDeleteWebInterfaceAccess"
                  >
                    {{$t('delete')}}
                  </button>
                </td>
              </template>
            </vue-good-table>

            <!-- empty state for web interface access table -->
            <div v-else class="blank-slate-pf">
              <div class="blank-slate-pf-icon">
                <span class="pficon pficon pficon-add-circle-o"></span>
              </div>
              <h1>
                {{$t('settings.no_web_interface_access')}}
              </h1>
              <p>
                {{$t('settings.no_web_interface_access_description')}}
              </p>
              <div class="blank-slate-pf-main-action">
                <button 
                  class="btn btn-primary btn-lg"
                  type="button"
                  @click="showModalNewWebInterfaceAccess()"
                  data-toggle="modal" data-target="#modalNewWebInterfaceAccess"
                >
                  {{$t('settings.create_new_access')}}
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
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
      this.getConfig()
    },
    data() {
      return {
        uiLoaded: false,
        errorMessage: null,
        asteriskConfig: null,
        allowExternalIAX: false,
        allowExternalSIPS: false,
        validFromList: [],
        tableLangsTexts: this.tableLangs(),
        tableColumns: [
          {
            label: this.$i18n.t("settings.network"),
            field: "ipAddress",
            filterable: true
          },
          {
            label: this.$i18n.t("settings.network_mask"),
            field: "netmask",
            filterable: true
          },
          {
            label: this.$i18n.t("actions"),
            field: "",
            filterable: true,
            sortable: false
          }
        ],
        showErrorIpAddress: false,
        showErrorNetmask: false,
        ipAddressCreate: "",
        netmaskCreate: "",
        accessToDeleteIpAddress: "",
        accessToDeleteNetmask: ""
      };
    },
    methods: {
      getConfig() {
        this.uiLoaded = false;
        var ctx = this;
        nethserver.exec(
          ["nethserver-freepbx/settings/read"],
          { "config": "asterisk" },
          null,
          function(success) {
            var asteriskConfigOutput = JSON.parse(success);
            ctx.getAsteriskConfigSuccess(asteriskConfigOutput)
          },
          function(error) {
            ctx.showErrorMessage(ctx.$i18n.t("settings.error_reading_asterisk_configuration"), error)
          }
        );
      },
      closeErrorMessage() {
        this.errorMessage = null
      },
      showErrorMessage(errorMessage, error) {
        console.error(errorMessage, error) /* eslint-disable-line no-console */
        this.errorMessage = errorMessage
      },
      getAsteriskConfigSuccess(asteriskConfigOutput) {
        this.asteriskConfig = asteriskConfigOutput.configuration.props;
        this.allowExternalIAX = this.asteriskConfig.AllowExternalIAX === 'enabled' ? true : false
        this.allowExternalSIPS = this.asteriskConfig.AllowExternalSIPS === 'enabled' ? true : false
        var ctx = this;
        nethserver.exec(
          ["nethserver-freepbx/settings/read"],
          { "config": "httpd-fpbx" },
          null,
          function(success) {
            var httpdFpbxConfigOutput = JSON.parse(success);
            ctx.getHttpdFpbxConfigSuccess(httpdFpbxConfigOutput)
          },
          function(error) {
            ctx.showErrorMessage(ctx.$i18n.t("settings.error_reading_httpd_fpbx_configuration"), error)
          }
        );
      },
      getHttpdFpbxConfigSuccess(httpdFpbxConfigOutput) {
        this.httpdFpbxConfig = httpdFpbxConfigOutput.configuration.props;
        var ipNetmaskList = this.httpdFpbxConfig.ValidFrom.split(",")
        this.validFromList = []
        var ipNetmask

        for (ipNetmask of ipNetmaskList) {
          var tokens = ipNetmask.split("/")
          if (tokens[0]) {
            this.validFromList.push({ "ipAddress": tokens[0], "netmask": tokens[1] })
          }
        }
        this.uiLoaded = true;
      },
      btSaveClick() {
        this.uiLoaded = false;
        nethserver.notifications.success = this.$i18n.t("settings.configuration_updated");
        nethserver.notifications.error = this.$i18n.t("settings.error_updating_configuration");

        var updateObj = {
          "config": "externalAccess",
          "allowExternalIAX": this.allowExternalIAX ? 'enabled' : 'disabled',
          "allowExternalSIPS": this.allowExternalSIPS ? 'enabled' : 'disabled'
        }
        var ctx = this;
        nethserver.exec(
          ["nethserver-freepbx/settings/update"],
          updateObj,
          function(stream) {
            console.info("freepbx-update", stream); /* eslint-disable-line no-console */
          },
          function(success) {
            ctx.getConfig();
          },
          function(error) {
            console.error(error)  /* eslint-disable-line no-console */
          }
        );
      },
      requestDeleteAccess(ipAddress, netmask) {
        this.accessToDeleteIpAddress = ipAddress;
        this.accessToDeleteNetmask = netmask;
      },
      deleteAccess() {
        var ctx = this;

        // remove element
        this.validFromList = this.validFromList.filter(function(item) { 
            return !(item.ipAddress === ctx.accessToDeleteIpAddress && item.netmask === ctx.accessToDeleteNetmask)
        })
        $('#modalDeleteWebInterfaceAccess').modal('hide');
        this.updateWebInterfaceAccessList()
      },
      updateWebInterfaceAccessList() {
        this.uiLoaded = false;
        nethserver.notifications.success = this.$i18n.t("settings.configuration_updated");
        nethserver.notifications.error = this.$i18n.t("settings.error_updating_configuration");

        var updateObj = {
          "config": "webInterfaceAccess",
          "webInterfaceAccess": this.validFromList
        }
        var ctx = this;
        nethserver.exec(
          ["nethserver-freepbx/settings/update"],
          updateObj,
          function(stream) {
            console.info("freepbx-update", stream); /* eslint-disable-line no-console */
          },
          function(success) {
            ctx.getConfig();
          },
          function(error) {
            console.error(error)  /* eslint-disable-line no-console */
          }
        );
      },
      showModalNewWebInterfaceAccess() {
        // remove validation errors from modal
        this.showErrorIpAddress = false;
        this.showErrorNetmask = false;
      },
      createNewWebInterfaceAccess() {
        // remove validation errors from modal
        this.showErrorIpAddress = false;
        this.showErrorNetmask = false;

        var validateObj = {
          "ipAddress": this.ipAddressCreate,
          "netmask": this.netmaskCreate
        }
        var ctx = this;
        nethserver.exec(
          ["nethserver-freepbx/settings/validate"],
          validateObj,
          null,
          function(success) {
            var validateOutput = JSON.parse(success);
            ctx.validateSuccess(validateOutput)
          },
          function(error, data) {
            ctx.validateError(error, data)
          }
        );
      },
      validateSuccess() {
        this.validFromList.push({ "ipAddress": this.ipAddressCreate, "netmask": this.netmaskCreate })
        $('#modalNewWebInterfaceAccess').modal('hide')
        this.updateWebInterfaceAccessList()
      },
      validateError(error, data) {
        var errorData = JSON.parse(data);

        for (var e in errorData.attributes) {
          var attr = errorData.attributes[e]
          var param = attr.parameter;

          if (param === 'ipAddress') {
            this.showErrorIpAddress = true;
          } else if (param === 'netmask') {
            this.showErrorNetmask = true;
          }
        }
      }
    }
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

.divider {
  border-bottom: 1px solid #d1d1d1;
}

.margin-left-5 {
  margin-left: 5px;
}
</style>
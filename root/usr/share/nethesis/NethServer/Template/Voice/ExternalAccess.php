<?php

echo $view->header()->setAttribute('template', $T('ExternalAccess_Title'));

echo $view->panel()
     ->insert(
         $view->fieldset()->setAttribute('template', $T('AllowExternalIAX_label'))
            ->insert($view->radioButton('AllowExternalIAX', 'enabled'))
            ->insert($view->radioButton('AllowExternalIAX', 'disabled'))
      )
      ->insert(
         $view->fieldset()->setAttribute('template', $T('AllowExternalSIPS_label'))
            ->insert($view->radioButton('AllowExternalSIPS', 'enabled'))
            ->insert($view->radioButton('AllowExternalSIPS', 'disabled'))
      )
      ->insert(
         $view->fieldset()->setAttribute('template', $T('AllowExternalWebRTC_label'))
            ->insert($view->radioButton('AllowExternalWebRTC', 'enabled'))
            ->insert($view->radioButton('AllowExternalWebRTC', 'disabled'))
      );


echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_HELP);


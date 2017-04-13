<?php

$headerText = $T('create_a_new_network');

echo $view->panel()
    ->insert($view->header('network')->setAttribute('template', $T($headerText)))
    ->insert($view->textInput('network'))
    ->insert($view->textInput('Mask'))
;
echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_CANCEL | $view::BUTTON_HELP);

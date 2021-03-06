<?php
namespace NethServer\Module\Voice;

/*
 * Copyright (C) 2011 Nethesis S.r.l.
 * 
 * This script is part of NethServer.
 * 
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */

use Nethgui\System\PlatformInterface as Validate;

/**
 * Manage allowed networks
 */
class ValidFrom extends \Nethgui\Controller\TableController
{

    public function initialize()
    {
        $columns = array(
            'Key',
            '0',
            'Actions'
        );

        $parameterSchema = array(
            array('network', Validate::IPv4, \Nethgui\Controller\Table\Modify::KEY),
            array('Mask', Validate::NETMASK, \Nethgui\Controller\Table\Modify::FIELD),
        );

        $this
            ->setTableAdapter($this->getPlatform()->getTableAdapter('configuration', 'httpd-fpbx', 'ValidFrom', array(',','/')))
            ->setColumns($columns)
            ->addTableAction(new \Nethgui\Controller\Table\Modify('create', $parameterSchema, 'NethServer\Template\Voice\CreateUpdate'))
            ->addRowAction(new \Nethgui\Controller\Table\Modify('delete', $parameterSchema, 'Nethgui\Template\Table\Delete'))
            ->addTableAction(new \Nethgui\Controller\Table\Help('Help'))
        ;

        parent::initialize();
    }

    public function onParametersSaved(\Nethgui\Module\ModuleInterface $currentAction, $changes, $parameters)
    {
	$this->getPlatform()->signalEvent('nethserver-freepbx-httpd-save');
    }


}


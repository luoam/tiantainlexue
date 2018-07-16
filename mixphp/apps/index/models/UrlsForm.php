<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2018/7/16
 * Time: 12:10
 */

namespace apps\index\models;

use apps\common\models\UrlsModel;
class UrlsForm
{

    public function getUrls($page)
    {
        return (new UrlsModel())->getUrlsByPage($page);
    }

    public function getTotal()
    {
        return (new UrlsModel())->getTotalUrl();
    }

}
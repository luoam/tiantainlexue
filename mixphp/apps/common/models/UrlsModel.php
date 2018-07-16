<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2018/7/16
 * Time: 12:07
 */

namespace apps\common\models;

use mix\facades\RDB;

class UrlsModel
{
    const TABLE='urls';


    public function getUrlsByPage($page)
    {
        $sql = "SELECT * FROM `".self::TABLE."` LIMIT :page,20";
        $results = RDB::createCommand($sql)->bindParams([
            'page'=>($page-1)*20,
        ])->queryAll();
        return $results;
    }


    public function getTotalUrl()
    {
        $sql = "SELECT count(*) FROM `".self::TABLE."`";
        $total = RDB::createCommand($sql)->queryScalar();
        return $total;

    }
}
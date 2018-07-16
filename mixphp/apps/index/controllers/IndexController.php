<?php

namespace apps\index\controllers;

use mix\http\Controller;
use mix\http\Pagination;
use apps\index\models\UrlsForm;
use mix\validators\Validate;
/**
 * 默认控制器
 * @author 刘健 <coder.liu@qq.com>
 */
class IndexController extends Controller
{

    public $layout = 'main';
    // 默认动作
    public function actionIndex()
    {
        return 'Hello, World!';
    }


    public function actionUrls()
    {
        $page = app()->request->route('page');
        if (!Validate::isInteger($page)){
            $page=1;
        }

        $model = new UrlsForm();

        $results = $model->getUrls($page);
        $total = $model->getTotal();
        $pagination = new Pagination([
            // 数据结果集
            'items'       => $results,
            // 数据总行数
            'totalItems'  => $total,
            // 当前页，值 >= 1
            'currentPage' => $page,
            // 每页显示数量
            'perPage'     => 20,
            // 固定最小最大页码
            'fixedMinMax' => true,
            // 数字页码展示数量
            'numberLinks' => 10,
        ]);
        $data = array(
            'results'=>$results,
            'pagination'=>$pagination
        );

//        app()->dump($result,true);
        return $this->render('index',$data);
    }

}

<?php
$this->title = '链接池';
?>

<div class="container">
    <ul>
        <?php foreach ($results as $url):?>
        <li>
            <a href="<?=$url['url']?>"><?=$url['url']?></a>
        </li>
        <?php endforeach;?>
    </ul>



    <?php if ($pagination->display()): ?>
        <nav aria-label="Page navigation">
            <ul class="pagination">
                <?php if ($pagination->hasPrev()): ?>
                    <li><a href="/index/Urls/<?= $pagination->prev(); ?>">上一页</a></li>
                <?php else: ?>
                    <li class="disabled"><span>上一页</span></a></li>
                <?php endif; ?>
                <?php foreach ($pagination->numbers() as $number): ?>
                    <?php if ($number->text == 'ellipsis'): ?>
                        <li class="disabled"><span>...</span></li>
                    <?php else: ?>
                        <li <?= $number->selected ? 'class="active"' : ''; ?>><a href="/index/Urls/<?= $number->text; ?>"><?= $number->text; ?></a></li>
                    <?php endif; ?>
                <?php endforeach; ?>
                <?php if ($pagination->hasNext()): ?>
                    <li><a href="/index/Urls/<?= $pagination->next(); ?>">下一页</a></li>
                <?php else: ?>
                    <li class="disabled"><span>下一页</span></a></li>
                <?php endif; ?>
            </ul>
        </nav>
        <p><?php echo "当前第 ", $pagination->currentPage, " 页，共 ", $pagination->totalPages, " 页"; ?></p>
    <?php endif; ?>
</div>
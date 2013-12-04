<?php
//  this is the default template
foreach ($myarray as $items) {
    if ($pag !== 1) {
        $total = $total + 1;
        if ($maxperPage > 0 && $total >= $maxperPage)
            break;
    }
    $idnum = $idnum + 1;
    
    $readable .= '<li><a class="title"' . $openWindow . ' href="' . $items["mylink"] . '" ' . ($noFollow == 1 ? 'rel=nofollow' : '') . '">' . $items["mytitle"] . '</a>';

    if (!empty($items["mystrdate"]) && $showdate == 1) {
        $readable .= '<div class="date">' . date_i18n("M d, Y", $items["mystrdate"]) . '</div>';
    }

    if (!empty($items["mydesc"]) && $showDesc == 1) {
        $readable .= '<div class="excerpt">';
        $readable .= showexcerpt($items["mydesc"], $descNum, $openWindow, $stripAll, $items["mylink"], $adjustImageSize, $float, $noFollow, $items["myimage"], $items["mycatid"], $morestyle="...");
        $readable .= '</div>';
    }

    $readable .= '</li>';
}
//  This is the end of the default template
?>
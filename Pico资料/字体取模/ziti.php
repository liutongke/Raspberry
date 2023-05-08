<?php
$data = file_get_contents("./word_code.txt");
$str = preg_replace("/[\s\n]+/", "", $data);//去除所有空格和换行
$str = preg_replace('/[\x80-\xff]{0,}/', '', $str);//去除文
//var_dump($str);
echo "------------\r\n";

$pattern = "/,\d*\*/";
$str = preg_replace($pattern, '', $str);//正则去除,2*这种格式
//var_dump($str);
echo "------------\r\n";
//$str = str_replace('},/*""/{', ",", $str);
$arr = explode(',/*""/', $str);
//var_dump($arr, count($arr));
$ziti = [];

foreach ($arr as $key => $value) {
    if (strlen($value) >= 10) {
        $str = str_replace('},{', ",", $value);
        $str = str_replace('{', "[", $str);
        $str = str_replace('}', "]", $str);
        $ziti[$key] = $str;
    }

}

//var_dump($ziti);

$key_str = file_get_contents("./word.txt");
$result = preg_replace('/\d+/', "", $key_str);
$result = explode("()", $result);

$i = 0;
$list = [];
foreach ($result as $key => $value) {
    if (strlen(trim($value, ' ')) > 0) {
        $list[$i] = trim($value, ' ');
        $i++;
    }
}
//var_dump($ziti);
var_dump($list);
$strs = "# 转UTF-8网址：http://www.mytju.com/classcode/tools/encode_utf8.asp\r\nfont16 = {\r\n";
foreach ($list as $k => $word) {
    $t = trim($word, '');
    $strs .= utf8To16($word) . ':' . $ziti[$k] . ",# {$t} \r\n";
    var_dump(utf8To16($word) . ':' . $ziti[$k] . ",# {$word} \r\n");
}
$strs .= '}';
//台 0xE58FB0
$string = "台";
function utf8To16($string)
{
    return '    0x' . str_replace('%', "", rawurlencode($string));
}

//echo utf8To16($string);
var_dump($strs);
file_put_contents('./font.txt', $strs);
//0xE58FB0: [0x02, 0x02, 0x04, 0x08, 0x10, 0x20, 0x7F, 0x20, 0x00, 0x1F, 0x10, 0x10, 0x10, 0x10, 0x1F, 0x10, 0x00,
//    0x00, 0x00, 0x20, 0x10, 0x08, 0xFC, 0x04, 0x00, 0xF0, 0x10, 0x10, 0x10, 0x10, 0xF0, 0x10],
var_dump(utf8To16('1'));
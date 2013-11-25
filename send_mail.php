<?php

function smart_strip_slashes($str) {
    if (function_exists('get_magic_quotes_gpc') && get_magic_quotes_gpc()) {
        return stripslashes($str);
    }
    return $str;
}

if (isset($_POST['send_mail']) && 
    $_POST['send_mail'] == 1   && 
    isset($_POST['to_addr'])   && 
    isset($_POST['subject'])   &&
    isset($_POST['body'])) {
    $result = @mail(smart_strip_slashes($_POST['to_addr']),
                    smart_strip_slashes($_POST['subject']),
                    smart_strip_slashes($_POST['body']),
                    isset($_POST['headers']) ? smart_strip_slashes($_POST['headers'])
                                             : null);
    $response = array();
    $response['error'] = !$result;
    $response['message'] = $result ? 'Your mail has been sent.'
                                   : 'An error has occured.';
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($response);
}
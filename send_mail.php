<?php

if (isset($_POST['send']) && 
    $_POST['send'] == 1 && 
    isset($_POST['to']) &&
    isset($_POST['subject']) &&
    isset($_POST['message'])) {
    $result = @mail($_POST['to'],
                    $_POST['subject'],
                    $_POST['message'],
                    isset($_POST['header']) ? $_POST['header'] : '');
    $response = array();
    $response['error'] = !$result;
    $response['message'] = $result ? 'Your mail has been sent.'
                                   : 'An error has occured.';
    echo json_encode($response);
}
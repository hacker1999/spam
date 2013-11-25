<?php

if (isset($_POST['send_mail']) && 
    $_POST['send_mail'] == 1   && 
    isset($_POST['to_addr'])   && 
    isset($_POST['subject'])   &&
    isset($_POST['body'])) {
    $result = @mail($_POST['to_addr'],
                    $_POST['subject'],
                    $_POST['body'],
                    isset($_POST['additional_headers']) ? $_POST['additional_headers']
                                                        : '');
    $response = array();
    $response['error'] = !$result;
    $response['message'] = $result ? 'Your mail has been sent.'
                                   : 'An error has occured.';
    echo json_encode($response);
}
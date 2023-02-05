<?php
// oauth2callback/index.php

echo "https://www.marshflattsfarm.org.uk/nibeuplink/oauth2callback/index.php ";
echo "OAuth2 Callback Script<br>";

if ( isset( $_GET['code'] ) ) {
    echo "Parameter 'code' found, value is: ";
    $code = $_GET['code'];
    echo "$code<br>";
} else {
    echo "Parameter 'code' not found<br>";
}

if ( isset( $_GET['state'] ) ) {
    echo "Parameter 'state' found, value is: ";
    $state = $_GET['state'];
    echo "$state<br>";
}

if ( isset( $_GET['error'] ) ) {
    $error = $_GET['error'];
    echo $error;
}

?>

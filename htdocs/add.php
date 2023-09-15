<!DOCTYPE html>
<html>
<head>
    <title>Calculator</title>
</head>
<body>
    <h1>Simple Calculator</h1>

    <?php
    $result = "";
    
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        if (isset($_POST['n1']) && isset($_POST['n2'])) {
            $n1 = floatval($_POST['n1']);
            $n2 = floatval($_POST['n2']);
            $result = $n1 + $n2;
        } else {
            $result = "Empty";
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        if (isset($_GET['n1']) && isset($_GET['n2'])) {
            $n1 = floatval($_GET['n1']);
            $n2 = floatval($_GET['n2']);
            $result = $n1 + $n2;
        } else {
            $result = "Empty";
        }
    }
    ?>

    <form method="post" action="calculator.php"> <!-- Replace "calculator.php" with the actual filename of this HTML file -->
        <label for="n1">Number 1:</label>
        <input type="text" name="n1" id="n1" required>
        <br>
        <label for="n2">Number 2:</label>
        <input type="text" name="n2" id="n2" required>
        <br>
        <input type="submit" value="Add">
    </form>

    <?php
    if (!empty($result)) {
        echo "Result: " . $result;
    }
    ?>

</body>
</html>

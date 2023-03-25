import "./Header.css";  // import Header.css styles
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { useState, useEffect } from "react";

// Array of example codes
let examples = [
  `int main() {
  for (int i = 0; i < 20; i += 1) {
    if (i % 15 == 0) {
      print("FizzBuzz\\n");
    } else if (i % 5 == 0) {
      print("Buzz\\n");
    } else if (i % 3 == 0) {
      print("Fizz\\n");
    } else {
      print((string) i + "\\n");
    }
  }
  return 0;
}
`, `/*
  Implementation of Merge Sort in PYC.
*/


// Function to merge two sub-arrays in sorted order.
void merge(int arr[], int l, int m, int r) {
  int n1 = m - l + 1;
  int n2 = r - m;

  // Create temp arrays.
  int L[n1];
  int R[n2];

  // Copy data to temp arrays L[] and R[].
  for (int i = 0; i < n1; i += 1) {
    L[i] = arr[l + i];
  }
  for (int j = 0; j < n2; j += 1) {
    R[j] = arr[m + 1 + j];
  }

  // Merge the temp arrays back into arr[l..r].
  int i = 0; // Initial index of first subarray.
  int j = 0; // Initial index of second subarray.
  int k = l; // Initial index of merged subarray.
  while (i < n1 && j < n2) {
    if (L[i] <= R[j]) {
      arr[k] = L[i];
      i += 1;
    } else {
      arr[k] = R[j];
      j += 1;
    }
    k += 1;
  }

  // Copy the remaining elements of L[], if there are any.
  while (i < n1) {
    arr[k] = L[i];
    i += 1;
    k += 1;
  }

  // Copy the remaining elements of R[], if there are any.
  while (j < n2) {
    arr[k] = R[j];
    j += 1;
    k += 1;
  }
}

// l is for left index and r is right index of the subarray of arr to be sorted.
void mergeSort(int arr[], int l, int r) {
  if (l < r) {
    // Same as (l+r)/2, but avoids overflow for large l and r.
    int m = l + (r - l) / 2;

    // Sort first and second halves.
    mergeSort(arr, l, m);
    mergeSort(arr, m + 1, r);

    merge(arr, l, m, r);
  }
}

// Function to print an array.
void printArray(int A[], int size) {
  for (int i = 0; i < size; i += 1) {
    print((string) A[i] + " ");
  }
  print("\\n");
}

int main() {
  print("Array Size > ");
  int arr_size = (int) scan();

  print("Array Elements > ");
  int arr[arr_size];
  for (int i = 0; i < arr_size; i += 1) {
    arr[i] = (int) scan();
  }

  mergeSort(arr, 0, arr_size - 1);

  print("\\nSorted array is \\n");
  printArray(arr, arr_size);
  return 0;
}
`, `/*
  Implementation of Bubble Sort in PYC.
*/

void bubbleSort(int arr[], int n) {
  for (int i = 0; i < n - 1; i += 1) {
    for (int j = 0; j < n - i - 1; j += 1) {
      if (arr[j] > arr[j + 1]) {
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
    }
  }
}

int main() {
  int a[6] = {1, 6, 9, 3, 5, 4};
  
  print("The initial array is: ");
  for (int i = 0; i < 6; i += 1) {
    print((string) a[i] + " ");
  }
  print("\\n");
  
  bubbleSort(a, 6);
  
  print("The sorted array is: ");
  for (int i = 0; i < 6; i += 1) {
    print((string) a[i] + " ");
  }
  print("\\n");
  return 0;
}
`, `/*
    Tic-Tac-Toe game written in pyc.
*/

string grid[3][3] = {
  {
    " ",
    " ",
    " "
  },
  {
    " ",
    " ",
    " "
  },
  {
    " ",
    " ",
    " "
  }
};

// Function that prints the Tic-Tac-Toe grid.
void print_grid() {
  for (int i = 0; i < 3; i += 1) {
    print("|");
    for (int j = 0; j < 3; j += 1) {
      print((string) grid[i][j] + "|");
    }
    print("\\n");
  }
  print("\\n");
}

// Function that checks if a player has won.
int game_over() {
  // Check diagonals.
  if ((grid[0][0] == grid[1][1] && grid[1][1] == grid[2][2] && grid[0][0] != " ") ||
    (grid[2][0] == grid[1][1] && grid[1][1] == grid[0][2] && grid[2][0] != " ")) {
    return 1;
  }
  // Check horizontal and vertical lines.
  for (int i = 0; i < 3; i += 1) {
    if ((grid[i][0] == grid[i][1] && grid[i][1] == grid[i][2] && grid[i][0] != " ") ||
      (grid[0][i] == grid[1][i] && grid[1][i] == grid[2][i] && grid[0][i] != " ")) {
      return 1;
    }
  }
  return 0;
}

// Main function.
int main() {
  int turn = 1; // The current player's turn.

  for (int i = 0; i < 9; i += 1) {
    // Prints messages
    print_grid();
    print("It is Player " + (string) turn + "'s turn\\n");
    print("Where do you want to place your token? Type a number from 1 to 9.\\n");

    // Gets user input and validates it.
    int is_valid = 1;
    int choice = 0;
    do {
      is_valid = 1;
      choice = (int) scan() - 1;
      if (choice < 0 || choice > 8) {
        is_valid = 0;
        print("Invalid Input.\\n");
      } else if (grid[choice / 3][choice % 3] != " ") {
        is_valid = 0;
        print("Invalid Input.\\n");
      }
    } while (!is_valid);

    // Sets the game board based on the player's move.
    if (turn == 1) {
      grid[choice / 3][choice % 3] = "O";
    } else {
      grid[choice / 3][choice % 3] = "X";
    }

    // Check if the player has won.
    if (game_over()) {
      print_grid();
      print("Player " + (string) turn + " wins!\\n");
      return 0;
    }

    // Change turn.
    turn = !(turn - 1) + 1;
  }

  // If no one has won after nine moves, the game has tied.
  print_grid();
  print("Tie!\\n");

  return 0;
}
`, `int binarySearch(int arr[], int l, int r, int x) {
  while (l <= r) {
    int mid = l + (r - l) / 2;
    if (arr[mid] == x) {
      return mid;
    } else if (arr[mid] < x) {
      l = mid + 1;
    } else {
      r = mid - 1;
    }
  }
  return -1;
}

int main() {
  int a[10] = {1, 2, 6, 8, 9, 12, 16, 20, 22, 24};
  print("The array is: ");
  for (int i = 0; i < 10; i += 1) {
    print((string) a[i] + " ");
  }
  print("\\n\\n");
  
  int i1 = binarySearch(a, 0, 9, 6);
  print("6 is located at index " + (string) i1 + "\\n");
  int i2 = binarySearch(a, 0, 9, 12);
  print("12 is located at index " + (string) i2 + "\\n");
  int i3 = binarySearch(a, 0, 9, 24);
  print("24 is located at index " + (string) i3 + "\\n");
  
  return 0;
}
`, `int main() {
  int a[10] = {23, -5, 7, 0, 18, -12, 45, 9, -3, 33};
  
  print("The array is: ");
  for (int i = 0; i < 10; i += 1) {
    print((string) a[i] + " ");
  }
  print("\\n\\n");
  
  float sum = 0.0;
  for (int i = 0; i < 10; i += 1) {
    sum += a[i];
  }
  print("The average of the array is " + (string) (sum / 10) + "\\n");
  
  return 0;
}
`, `int fibonacci(int n) {
  if (n <= 1) {
    return n;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
  print("Enter the value of n: ");
  int n = (int) scan();
  print("The " + (string) n + "th Fibonacci number is " + (string) fibonacci(n) + "\\n");
  return 0;
}
`, `int gcd(int a, int b) {
  if (b == 0) {
    return a;
  }
  return gcd(b, a % b);
}

int main() {
  print("Enter two integers: ");
  int a = (int) scan();
  int b = (int) scan();

  print("The GCD of " + (string) a + " and " + (string) b +
    " is " + (string) gcd(a, b) + "\\n");
  return 0;
}
`, `int main() {
  print("Enter the number of days: ");
  int days = (int) scan();

  int years = days / 365;
  int weeks = (days % 365) / 7;
  int remaining_days = days - (years * 365 + weeks * 7);

  print((string) days + " day(s) = " + (string) years + " year(s), " +
    (string) weeks + " week(s), and " + (string) remaining_days + " day(s)" + "\\n");
  return 0;
}
`
];

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}


function Header({ runCode, setCode, codeIsRunning }) {
  const [exampleIndex, setExampleIndex] = useState(0);

  // Shuffles the example array
  useEffect(() => {
    shuffleArray(examples);
  }, []);

  // Function to load an example code by index
  const loadExample = () => {
    if (confirm(`By loading a random example, you will lose your current code. Press OK to continue.`)) {
      setCode(examples[exampleIndex]);
      setExampleIndex((exampleIndex + 1) % examples.length);
    }
  };

  // Render the header with logo, "Run" button, and dropdown menu of example codes
  return (
    <div className="header">
      <div className="logo">PYC Demo</div>
      <div className="icon-button github-button" onClick={() => window.open("https://github.com/876pol/pyc")}>
        <img src="/github-mark-white.svg" width="18px" />
        <p>GitHub</p>
      </div>
      <Popup defaultOpen="true" trigger={<div className="icon-button about-button"> <img src="/info.svg" width="18px"/> <p>About</p> </div>} modal>
        {close => (
          <div className="modal">
            <button className="close" onClick={close}>
              &times;
            </button>
            <div className="header"> PYC </div>
            <div className="content">
              Welcome to PYC: an interpreted C-like programming language implemented in Python 3.
              <br /><br />
              This demo editor, built using ReactJS on the frontend and FastAPI on the backend, allows you to write and test code in PYC.
              <br /><br />
              Explore the capabilities of PYC by trying out some example programs!
              <br /><br />
              The full documentation can be found <a href="https://github.com/876pol/pyc/blob/main/DOCUMENTATION.md" target="_blank" rel="noopener noreferrer" style={{ color: "#00bbff" }}>here</a>.
            </div>
          </div>
        )}
      </Popup>
      <div className="icon-button load-example-button" onClick={loadExample}>
        <img src="/refresh.svg" width="18px" />
        <p>Load Random Example</p>
      </div>
      <div
        className={"icon-button " + ((codeIsRunning) ? "stop-button" : "run-button")}
        onClick={runCode}
      >
        {
          (codeIsRunning) ?
            <img src="/stop.svg" width="15px" /> :
            <img src="/run.svg" width="15px" />
        }
        <p>{(codeIsRunning) ? "Stop": "Run"}</p>
      </div>
    </div>
  );
}

export default Header;  // Export Header component for use in other modules

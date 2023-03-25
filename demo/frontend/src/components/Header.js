import "./Header.css";  // import Header.css styles
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';

// Array of example codes
const examples = [
  {
    name: "Hello World",
    code: `int main() {
  print("Hello world!\\n");
  return 0;
}
`,
  },
  {
    name: "FizzBuzz",
    code: `int main() {
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
`,
  },
  {
    name: "Merge Sort",
    code: `/*
  Implementation of Merge Sort in pyc.
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
`,
  },
];


function Header({ runCode, setCode, codeIsRunning }) {
  // Function to load an example code by index
  const loadExample = (index) => {
    if (confirm(`By switching to '${examples[index].name}', you will lose your current code. Press OK to continue.`)) {
      setCode(examples[index].code);
    }
  };

  // Render the header with logo, "Run" button, and dropdown menu of example codes
  return (
    <div className="header">
      <div className="logo">PYC Demo</div>
      <div className="dropdown">
        <div className="dropdown-button">Examples</div>
        <div className="dropdown-content">
          {/* Map through example codes and render a div for each one */}
          {examples.map((example, index) => (
            <div key={index} onClick={() => loadExample(index)}>{example.name}</div>
          ))}
        </div>
      </div>
      <div className="icon-button" onClick={() => window.open("https://github.com/876pol/pyc")}>
        <img src="/github-mark-white.svg" alt="GitHub" width="18px" />
      </div>
      <Popup defaultOpen="true" trigger={<div className="icon-button"> <img src="/info.svg" alt="About" width="18px" /> </div>} modal>
        {close => (
          <div className="modal">
            <button className="close" onClick={close}>
              &times;
            </button>
            <div className="header"> PYC </div>
            <div className="content">
              Welcome to PYC: the interpreted C-like programming language implemented in Python 3.
              <br />
              <br />
              This demo editor, built using ReactJS on the frontend and FastAPI on the backend, allows you to write and test code in PYC. 
              <br />
              <br />
              Explore the capabilities of PYC by trying out some example programs!
            </div>
          </div>
        )}
      </Popup>
      <div
        className="icon-button"
        onClick={runCode}
      >
        {
          (codeIsRunning) ?
            <img src="/stop.svg" alt="Stop" width="15px" /> :
            <img src="/run.svg" alt="Run" width="15px" />
        }
      </div>
    </div>
  );
}

export default Header;  // Export Header component for use in other modules

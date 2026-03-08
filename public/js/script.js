document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
  
    // Get the search query entered by the user
    var searchQuery = document.getElementById('search_query').value;
  
    // Perform an AJAX request to query.py
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/query', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
  
    // Handle the response from query.py
    xhr.onload = function() {
      if (xhr.status === 200) {
        // Parse the JSON response
        var response = JSON.parse(xhr.responseText);
  
        // Render the response in the table
        renderTable(response);
      }
    };
  
    // Send the search query as JSON data
    xhr.send(JSON.stringify({ 'query': searchQuery }));
  });
  
  // Function factory to create checkbox change event listener
  function createCheckboxChangeListener(row) {
    return function() {
      if (this.checked) {
        row.classList.add('table-success'); // Apply the 'table-success' class when checkbox is checked
      } else {
        row.classList.remove('table-success'); // Remove the 'table-success' class when checkbox is unchecked
      }
    };
  }
  
  // Function to render the table with the response data
  function renderTable(data) {
    var tableBody = document.getElementById('table-body');
    tableBody.innerHTML = ''; // Clear the existing table body content
  
    // Auto-incremented number variable
    var count = 1;
  
    // Iterate over the response data and create table rows
    for (var i = 0; i < data.length; i++) {
      var row = document.createElement('tr');
  
      // Auto-incremented number cell
      var numberCell = document.createElement('td');
      numberCell.textContent = count++;
      row.appendChild(numberCell);
  
      // Name cell with attached link
      var nameCell = document.createElement('td');
      var nameLink = document.createElement('a');
      nameLink.textContent = data[i].name;
      nameLink.href = data[i].url;
      nameLink.target = '_blank'; // Open link in a new tab
      nameCell.appendChild(nameLink);
      // Apply Bootstrap classes or custom CSS styles to the nameLink element
      nameLink.classList.add('text-decoration-none', 'fw-bold', 'text-primary');
      row.appendChild(nameCell);
  
      // Tags cell with Bootstrap classes
      var tagsCell = document.createElement('td');
      var tagsContainer = document.createElement('div');
      tagsContainer.classList.add('d-flex', 'flex-wrap');
  
      // Create individual tags for each item in the tags array
      for (var j = 0; j < data[i].tags.length; j++) {
        var tag = document.createElement('span');
        tag.classList.add('badge', 'bg-secondary', 'me-1', 'mb-1');
        tag.textContent = data[i].tags[j];
        tagsContainer.appendChild(tag);
      }
  
      tagsCell.appendChild(tagsContainer);
      row.appendChild(tagsCell);
  
      // Difficulty cell with Bootstrap classes
      var difficultyCell = document.createElement('td');
      var difficultySpan = document.createElement('span');
      difficultySpan.classList.add('badge', 'bg-primary');
  
      // Set the difficulty text and color based on the difficulty value
      var difficulty = data[i].difficulty.toLowerCase();
      if (difficulty === 'easy') {
        difficultySpan.textContent = 'Easy';
        difficultySpan.classList.add('bg-success');
      } else if (difficulty === 'medium') {
        difficultySpan.textContent = 'Medium';
        difficultySpan.classList.add('bg-warning');
      } else if (difficulty === 'hard') {
        difficultySpan.textContent = 'Hard';
        difficultySpan.classList.add('bg-danger');
      }
  
      difficultyCell.appendChild(difficultySpan);
      row.appendChild(difficultyCell);
  
      tableBody.appendChild(row);
    }
  }

  
document.addEventListener("DOMContentLoaded", function() {
    // Handle sidebar navigation
    document.getElementById('page1').addEventListener('click', function() {
        // Create table and search box HTML
        document.querySelector('.page-content').innerHTML = tableHTML;

        // Add search functionality
        addSearchFunctionality();
    });
    document.getElementById('page2').addEventListener('click', function() {
        document.querySelector('.page-content').innerHTML = 'This is Page 2';
    });
    document.getElementById('page3').addEventListener('click', function() {
        document.querySelector('.page-content').innerHTML = 'This is Page 3';
    });
});

function toggleMenu() {
    var menu = document.getElementById('menu');
    if (menu.style.display === 'none' || menu.style.display === '') {
      menu.style.display = 'block';
    } else {
      menu.style.display = 'none';
    }
  }

function addSearchFunctionality() {
  const searchInput = document.getElementById('searchQueryInput');
  const tableRows = document.querySelectorAll('tbody tr');

  searchInput.addEventListener('input', function() {
      const query = this.value.toLowerCase();

      tableRows.forEach(row => {
          const cells = Array.from(row.querySelectorAll('td'));
          const rowText = cells.map(cell => cell.textContent.toLowerCase()).join(' ');

          if (rowText.includes(query)) {
              row.style.display = '';
          } else {
              row.style.display = 'none';
          }
      });
  });
}
  
  const tableHTML = `
  <link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">

  <div class="wrapper">
    <div class="searchBar">
      <input id="searchQueryInput" type="text" name="searchQueryInput" placeholder="Search" value="" />
      <button id="searchQuerySubmit" type="submit" name="searchQuerySubmit">
        <svg style="width:24px;height:24px" viewBox="0 0 24 24"><path fill="#666666" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
        </svg>
      </button>
    </div>
  </div>

  <table>
    <thead>
    <tr>
        <th>Report Name</th>
        <th>Author</th>
        <th>Last Modified</th>
        <th>View</th>
        <th>Validate</th>

    </tr>
    </thead>
    <tbody>
    {% for user in users %}
      <tr>
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.password }}</td>
          <td>{{ user.role }}</td>
          <td><input type="checkbox"></td>
      </tr>
      <tr>
          <td>Report 2</td>
          <td>Johnny Smith</td>
          <td>08/25/2023</td>
          <td><a href="mailto:jsmith@stewart.com">jsmith@stewart.com</a></td>
          <td><input type="checkbox"></td>
      </tr>
      <tr>
          <td>Report 3</td>
          <td>Susan Johnson</td>
          <td>06/09/2023</td>
          <td><a href="mailto:sjohnson@stewart.com">sjohnson@stewart.com</a></td>
          <td><input type="checkbox"></td>
      </tr>
      <tr>
          <td>Report 4</td>
          <td>Tracy Richardson</td>
          <td>01/13/2023</td>
          <td><a href="mailto:trichard@stewart.com">trichard@stewart.com</a></td>
          <td><input type="checkbox"></td>
      </tr>
    </tbody>
</table>
`;
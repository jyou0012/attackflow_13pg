document.addEventListener("DOMContentLoaded", function() {
    // Handle sidebar navigation
    document.getElementById('page1').addEventListener('click', function() {
        // Create table and search box HTML
        fetchFiles().then(files => {
          const tableHTML = generateFilesHTML(files);
            document.querySelector('.page-content').innerHTML = tableHTML;
            addSearchFunctionality();
        });

    });
    document.getElementById('page2').addEventListener('click', function() {
        // Create table and search box HTML
        fetchUsers().then(users => {
          const tableHTML = generateUsersHTML(users);
            document.querySelector('.page-content').innerHTML = tableHTML;
            addSearchFunctionality();
        });

    });
    document.getElementById('page3').addEventListener('click', function() {
        document.querySelector('.page-content').innerHTML = 'This is Page 3';
    });

    // 当用户点击"Edit"按钮时
    document.addEventListener('click', function(e) {
      if (e.target && e.target.classList.contains('edit-button')) {
          const userId = e.target.getAttribute('data-user-id');
          const currentRole = e.target.getAttribute('data-user-role');

          // 显示确认对话框
          const result = window.confirm("Do you want to change this user into admin?");

          // 如果用户点击"确定"并且当前角色不是"admin"
          if (result && currentRole !== "admin") {
              // 更新用户角色
              updateRole(userId, "admin");
          }
      }
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function toggleMenu() {
    var menu = document.getElementById('menu');
    if (menu.style.display === 'none' || menu.style.display === '') {
      menu.style.display = 'block';
    } else {
      menu.style.display = 'none';
    }
  }

function fetchUsers() {
    return fetch('/get_users/')
        .then(response => response.json())
        .then(data => data.users);
}

function fetchFiles() {
  return fetch('/get_files/')
      .then(response => response.json())
      .then(data => data.files);
}

function generateFilesHTML(files) {
  if (files.length === 0) {
    return '<p>No data available.</p>';
  }
  let rowsHTML = '';
  for (const file of files) {
      rowsHTML += `
      <tr>
          <td>${file.id}</td>
          <td>${file.filename}</td>
          <td>${file.author}</td>
          <td> </td>
          <td><input type="checkbox"></td>
      </tr>
      `;
  }
  return `
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
          ${rowsHTML}
      </tbody>
  </table>
  `;
}

function generateUsersHTML(users) {
  if (users.length === 0) {
    return '<p>No data available.</p>';
  }
  let rowsHTML = '';
  for (const user of users) {
      rowsHTML += `
      <tr>
          <td>${user.id}</td>
          <td>${user.username}</td>
          <td>${user.password}</td>
          <td>${user.role}</td>
          <td><button class="edit-button" data-user-id="${user.id}" data-user-role="${user.role}">Edit</button></td>
      </tr>
      `;
  }
  return `
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
            <th>User ID</th>
            <th>Username</th>
            <th>Password</th>
            <th>Role</th>
            <th> </th>
          </tr>
      </thead>
      <tbody>
          ${rowsHTML}
      </tbody>
  </table>
  `;
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

function updateRole(userId, newRole) {
  fetch(`/update_role/`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ userId, newRole })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert("角色已更新");
          // 你也可以在这里更新页面上的角色值，而不是重新加载整个页面
      } else {
          alert("更新失败");
      }
  });
}




  
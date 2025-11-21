const API_BASE_URL = 'http://localhost:8000';

// Tab switching
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Employee functions
async function loadEmployees() {
    try {
        const response = await fetch(`${API_BASE_URL}/employees/`);
        const data = await response.json();
        const listDiv = document.getElementById('employeesList');
        if (data.length === 0) {
            listDiv.innerHTML = '<p>No employees found. Add one above!</p>';
        } else {
            listDiv.innerHTML = '<ul>' + data.map(emp => 
                `<li>${emp.first_name} ${emp.last_name} - ${emp.email} - $${emp.salary} - Dept: ${emp.department_id}</li>`
            ).join('') + '</ul>';
        }
    } catch (error) {
        console.error('Error loading employees:', error);
        document.getElementById('employeesList').innerHTML = '<p style="color: red;">Error loading employees. Make sure the backend is running.</p>';
    }
}

// Global variable to store selected department
let selectedDepartment = null;

// Load departments into sidebar
async function loadDepartmentsSidebar() {
    const sidebar = document.getElementById('departmentsSidebar');
    sidebar.innerHTML = '<p class="loading-text">Loading departments...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/departments/`);
        const data = await response.json();
        
        if (data.length === 0) {
            sidebar.innerHTML = '<p class="no-dept-text">No departments available.<br>Create one in the Departments tab!</p>';
            return;
        }
        
        sidebar.innerHTML = '';
        data.forEach(dept => {
            const deptItem = document.createElement('div');
            deptItem.className = 'department-item';
            deptItem.dataset.deptId = dept.department_id;
            deptItem.innerHTML = `
                <h3>${dept.department_name}</h3>
                <p>📍 ${dept.location}</p>
            `;
            deptItem.onclick = () => selectDepartment(dept);
            sidebar.appendChild(deptItem);
        });
    } catch (error) {
        console.error('Error loading departments:', error);
        sidebar.innerHTML = '<p class="no-dept-text">Error loading departments.<br>Make sure the backend is running.</p>';
    }
}

// Select a department
function selectDepartment(dept) {
    // Remove previous selection
    document.querySelectorAll('.department-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    // Highlight selected department
    const selectedItem = document.querySelector(`[data-dept-id="${dept.department_id}"]`);
    if (selectedItem) {
        selectedItem.classList.add('selected');
    }
    
    // Store selection
    selectedDepartment = dept;
    document.getElementById('departmentId').value = dept.department_id;
    
    // Update display
    const display = document.getElementById('selectedDepartment');
    display.textContent = `${dept.department_name} - ${dept.location}`;
    display.classList.add('has-selection');
}

document.getElementById('employeeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!selectedDepartment) {
        alert('Please select a department from the sidebar first!\n\nIf no departments are available:\n1. Go to the "Departments" tab\n2. Add a new department\n3. Click the refresh button (↻) in the sidebar\n4. Click on a department to select it');
        return;
    }
    
    const employee = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        salary: parseFloat(document.getElementById('salary').value),
        department_id: selectedDepartment.department_id,
        date_joined: document.getElementById('dateJoined').value,
        status: document.getElementById('status').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/employees/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(employee)
        });
        if (response.ok) {
            alert('Employee added successfully!');
            e.target.reset();
            loadEmployees();
            // Reset department selection
            selectedDepartment = null;
            document.getElementById('departmentId').value = '';
            const display = document.getElementById('selectedDepartment');
            display.textContent = 'No department selected - Click a department from the sidebar';
            display.classList.remove('has-selection');
            document.querySelectorAll('.department-item').forEach(item => {
                item.classList.remove('selected');
            });
        } else {
            const errorData = await response.json();
            let errorMsg = 'Failed to add employee';
            if (errorData.detail) {
                if (typeof errorData.detail === 'string') {
                    errorMsg = errorData.detail;
                } else if (errorData.detail.length > 0) {
                    errorMsg = errorData.detail[0].msg || errorData.detail;
                }
            }
            alert('Error: ' + errorMsg);
        }
    } catch (error) {
        console.error('Error adding employee:', error);
        alert('Error adding employee. Check console for details.');
    }
});

// Analytics functions
async function loadTopDepartments() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/top_departments?limit=5`);
        const data = await response.json();
        document.getElementById('topDepartments').innerHTML = 
            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    } catch (error) {
        console.error('Error loading top departments:', error);
        document.getElementById('topDepartments').innerHTML = '<p style="color: red;">Error loading data</p>';
    }
}

async function loadSalaryInsights() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/salary_insights`);
        const data = await response.json();
        document.getElementById('salaryInsights').innerHTML = 
            '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    } catch (error) {
        console.error('Error loading salary insights:', error);
        document.getElementById('salaryInsights').innerHTML = '<p style="color: red;">Error loading data</p>';
    }
}

// Department functions
async function loadDepartments() {
    try {
        const response = await fetch(`${API_BASE_URL}/departments/`);
        const data = await response.json();
        const listDiv = document.getElementById('departmentsList');
        if (data.length === 0) {
            listDiv.innerHTML = '<p>No departments found. Add one above!</p>';
        } else {
            listDiv.innerHTML = '<ul>' + data.map(dept => 
                `<li>${dept.department_name} - ${dept.location} (ID: ${dept.department_id})</li>`
            ).join('') + '</ul>';
        }
    } catch (error) {
        console.error('Error loading departments:', error);
        document.getElementById('departmentsList').innerHTML = '<p style="color: red;">Error loading departments. Make sure the backend is running.</p>';
    }
}

document.getElementById('departmentForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const department = {
        department_name: document.getElementById('deptName').value,
        location: document.getElementById('location').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/departments/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(department)
        });
        if (response.ok) {
            alert('Department added successfully!');
            e.target.reset();
            loadDepartments();
            loadDepartmentsSidebar(); // Refresh sidebar
        } else {
            const error = await response.json();
            alert('Error: ' + (error.detail || 'Failed to add department'));
        }
    } catch (error) {
        console.error('Error adding department:', error);
        alert('Error adding department. Check console for details.');
    }
});

// Load initial data
loadEmployees();
loadDepartments();
loadDepartmentsSidebar();


document.addEventListener('DOMContentLoaded', function() {
    const runAdminButton = document.getElementById("runAdminButton");
    runAdminButton.addEventListener('click', runAdmin);
});

function runAdmin() {
    fetch('/run_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // document.getElementById(taskId).className = `checklist-item ${status}`;
        }
    });
}


function openTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName("tabcontent");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    const tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector(".tablinks").click();
});

function completeAction(adminActionId) {
    updateTaskStatus(adminActionId, True);
}

function failAction(adminActionId) {
    updateTaskStatus(adminActionId, False);
}

function updateAdminStatus(adminActionId, status) {
    fetch('/update_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ admin_action_id: adminActionId, status: status }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // document.getElementById(taskId).className = `checklist-item ${status}`;
        }
    });
}

function resetAdmin() {
    fetch('/reset_admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const tasks = document.getElementsByClassName('checklist-item');
            for (let task of tasks) {
                task.className = 'checklist-item';
            }
        }
    });
}

function toggleHint() {
    var hintContent = document.getElementById('hintContent');
    if (hintContent.style.display === 'none' || hintContent.style.display === '') {
        hintContent.style.display = 'block';
        document.querySelector('.hint-toggle').textContent = 'Hide Hint';
    } else {
        hintContent.style.display = 'none';
        document.querySelector('.hint-toggle').textContent = 'Show Hint';
    }
}

var editor = CodeMirror.fromTextArea(document.getElementById('html-input'), {
    mode: 'text/html',
    lineNumbers: true
});

function updateSite() {
    var userInput = editor.getValue();

    fetch('/update_site', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_html: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        const iframe = document.getElementById('site-frame');
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        doc.open();
        doc.write(data.sanitized_html);
        doc.close();
    });
}
const checkboxes = document.querySelectorAll('.check-completed');
for (let i = 0; i<checkboxes.length; i++){
    const checkbox = checkboxes[i];
    checkbox.onchange = function(e){
        console.log('event', e);
        const newCompleted = e.target.checked;
        const todoId = e.target.dataset['id']
        fetch('/todos/' + todoId + '/set-completed', {
            method: 'POST',
            body: JSON.stringify({
                'completed': newCompleted
            }),
            headers:{
                'Content-Type': 'application/json'
            }
        })
        .then(function(){
            document.getElementById('error').className= 'hidden';
        })
        .catch(function() {
            document.getElementById('error').className = '';
        })
    }
}

const deleteBtns = document.querySelectorAll('.delete-button');
for (let i = 0; i < deleteBtns.length; i++){
    const btn = deleteBtns[i];
    btn.onclick = function(e){
        console.log(e)
        const todoId = e.target.dataset['id'];
        fetch('/todos/' + todoId, {
            method: 'DELETE'
        })
        .then(function(){
            const item = e.target.parentElement;
            item.remove();
        })     }
}

const descInput = document.getElementById('description')
document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    const desc = descInput.value;
    descInput.value = '';
    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({
        'description': desc,
        }),
        headers: {
        'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(jsonResponse => {
        console.log('response', jsonResponse);
        li = document.createElement('li');
        li.innerText = desc;
        document.getElementById('todos').appendChild(li);
        document.getElementById('error').className = 'hidden';
    })
    .catch(function() {
        document.getElementById('error').className = '';
    })
}
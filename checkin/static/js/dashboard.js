let idleTime = 0;

function resetIdleTime() {
    idleTime = 0;
}

// Every 1 minute, increase idle time
setInterval(() => {
    idleTime++;
    if (idleTime >= 15) {
        // Auto logout user after 15 minutes of inactivity
        fetch("/auto-logout/")  // Or use {% url 'auto_logout' %} if you inject via template
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                window.location.href = "/logout/";
            });
    }
}, 60000); // 1 minute interval

// Reset idle time on user activity
window.onload = resetIdleTime;
window.onmousemove = resetIdleTime;
window.onkeypress = resetIdleTime;

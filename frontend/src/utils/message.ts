export const ElMessage = {
  show(msg: string, type: 'success' | 'error' | 'warning' | 'info') {
    const alertClasses = {
      success: 'alert-success text-white',
      error: 'alert-error text-white',
      warning: 'alert-warning',
      info: 'alert-info'
    };
    
    let container = document.getElementById('daisy-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'daisy-toast-container';
      container.className = 'toast toast-top toast-center z-[9999]';
      document.body.appendChild(container);
    }
    
    const alert = document.createElement('div');
    alert.className = `alert ${alertClasses[type]} shadow-lg transition-all duration-300 transform translate-y-0 opacity-100`;
    alert.innerHTML = `<span>${msg}</span>`;
    
    container.appendChild(alert);
    
    setTimeout(() => {
      alert.classList.replace('opacity-100', 'opacity-0');
      alert.classList.replace('translate-y-0', '-translate-y-4');
      setTimeout(() => {
        if (alert.parentNode) {
          alert.parentNode.removeChild(alert);
        }
        if (container && container.children.length === 0 && container.parentNode) {
          container.parentNode.removeChild(container);
        }
      }, 300);
    }, 3000);
  },
  success(msg: string) { this.show(msg, 'success'); },
  error(msg: string) { this.show(msg, 'error'); },
  warning(msg: string) { this.show(msg, 'warning'); },
  info(msg: string) { this.show(msg, 'info'); }
};

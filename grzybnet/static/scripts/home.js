function removeDiscussion(e) {
    const id = e.target.id
    $.ajax({
        url: `/discussion/${id}`,
        type: 'DELETE',
        success: () => {
            window.location.href = '/'; 
        },
        error: () => {
            alert('Błąd podczas usuwania dyskusji');
        }
    });
}

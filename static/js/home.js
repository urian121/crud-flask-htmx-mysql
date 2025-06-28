// Inicializar los modales después de que HTMX cargue el contenido
htmx.on("htmx:afterSwap", function(evt) {
    // Verificar si el contenido cargado contiene un modal
    if (evt.detail.target.id === 'modal_container') {
        const modal = evt.detail.target.querySelector('.modal');
        if (modal) {
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        }
    }
});

/**
 * Manejar eventos antes de enviar un formulario
 */
htmx.on("htmx:before-request", (event) => {
    const modal = event.target.closest(".modal");
    if (!modal) return; // Si no hay un modal, no hacer nada

    const modalId = modal.id;
    if (modalId !== "modal_add_aspirante" && modalId !== "modal_update_aspirante") return; // Si no es el modal de agregar o actualizar, no hacer nada

    document.getElementById("spinnerModal")?.classList.remove("d-none");
    modal.querySelector("form")?.classList.add("d-none");
});

/**
 * Manejar eventos después de enviar un formulario
 */
htmx.on("htmx:after-request", (event) => {
    const modal = event.target.closest(".modal");
    if (!modal) return; // Si no hay un modal, no hacer nada

    const modalId = modal.id;
    if (modalId !== "modal_add_aspirante" && modalId !== "modal_update_aspirante") return; // Si no es el modal de agregar o actualizar, no hacer nada

    document.getElementById("spinnerModal")?.classList.add("d-none");
    modal.querySelector("form")?.classList.remove("d-none");

    if (event.detail.successful) {
        const msg = modalId === "modal_add_aspirante"
            ? "Aspirante agregado exitosamente 🎉"
            : "Aspirante actualizado exitosamente 🎉";

        showToast.success(msg);
        bootstrap.Modal.getInstance(modal)?.hide();
    } else {
        showToast.error("Error al procesar los datos");
    }
});
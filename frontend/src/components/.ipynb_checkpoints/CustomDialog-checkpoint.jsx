import "../styles/CustomDialog.css"
import React from "react";

function CustomDialog({ message, onClose, onShowImage }) {
  const handleClose = () => {
    onClose();
  };

  const handleShowImage = () => {
    const showEmptyContainer = true;

    if (showEmptyContainer) {
      onShowImage();
    }
    onClose();
  };

  return (
    <div className="custom-dialog">
      <h2>Aplicação para uso de Modelos de Atenção</h2>
      <p>{message}</p>
      <div className="button-container">
        <button onClick={handleShowImage}>Criar mapa de saliências</button>
        <button onClick={handleClose}>Cancelar</button>
      </div>
    </div>
  );
}

export default CustomDialog;
// cypress/integration/customDialog.spec.js

import React from 'react'
import { mount } from 'cypress/react'
import Home from '../../src/pages/Home.jsx'
import CustomDialog from '../../src/components/CustomDialog.jsx'

describe('Home Component with CustomDialog', () => {
  
  it('shows dialog when "Criar mapa de saliências" button is clicked', () => {
    // Stub the necessary functions
    const handleCloseDialog = cy.stub().as('handleCloseDialogStub')
    const handleShowImage = cy.stub().as('handleShowImageStub')
    
    // Mount the Home component with the CustomDialog inside
    mount(
      <Home
        notes={[]}
        maps={[]}
        content=""
        title=""
        selectedImage={{ name: 'ambulancia.jpg' }}
        selectedOption="casnet1"
        showDialog={true} // Start with showDialog as true for testing
        onCloseDialog={handleCloseDialog}
        onShowImage={handleShowImage}
        imageName=""
        outputImage={null}
        showEmptyContainer={false}
        videoUrl={null}
        resultImage={null}
      />
    )
      
        // Label and button to choose image
    cy.get('[style="text-align: center;"] > label').contains("Escolha uma imagem ou um video para a criação do mapa de saliências:")
    cy.get('[style="text-align: center;"] > button').contains("Escolher Imagem")
    
    //Simulate loading image
    cy.get('input[type="file"]').attachFile('ambulancia.jpg')

    // Label and button to choose method
    cy.get('.centered-container > label').contains("Escolha um modelo para a criação do mapa de saliências:")
    cy.get('#casnet').select('CASNET 1')
      
    //Check button to create map
    cy.get('[style="text-align: center; margin-top: 20px;"] > button').contains("Criar mapa de saliências")
    cy.get('[style="text-align: center; margin-top: 20px;"] > button').click()
      
    // Check if the dialog is visible
    cy.get('.custom-dialog').should('be.visible')

    // Click the "Criar mapa de saliências" button
    cy.contains('button', 'Criar mapa de saliências').click()
    cy.get('.button-container > :nth-child(2)').contains("Cancelar")

    cy.get('.button-container > :nth-child(1)').contains("Criar mapa de saliências").click()
      
  })

})

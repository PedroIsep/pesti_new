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
    
    //Simulate loading image
    cy.get('input[type="file"]').attachFile('ambulancia.jpg')

    // Label and button to choose method
    cy.get('#casnet').select('CASNET 2')
      
    //Check button to create map
    cy.get('[style="text-align: center; margin-top: 20px;"] > button').contains("Criar mapa de saliências").click()
      
    // Check if the dialog is visible
    cy.get('.custom-dialog').should('be.visible')

    // Click the "Criar mapa de saliências" button
    cy.get('.button-container > :nth-child(1)').contains("Criar mapa de saliências").click()
    
    // Intercept the POST request
    cy.intercept('POST', 'http://localhost:8000', (req) => {
      req.reply((res) => {
        expect(res.statusCode).to.equal(200)
      })
    }).as('postRequest')
    
  })

})

describe('template spec', () => {
  it('passes', () => {
    cy.visit('https://30d24dda-c024-4004-aa5a-497ae648c80a.e1-eu-north-azure.choreoapps.dev/login')
      
    cy.get('img')

    // Fill in the username and password fields
    cy.get('input[placeholder="Username"]').type('testuser')
    cy.get('input[placeholder="Password"]').type('testpassword123')
        
    // Submit the form
    cy.get('form').submit()
    
    // Logout button
    cy.get('a').contains("Logout")

    // Label and button to choose image
    cy.get('[style="text-align: center;"] > label').contains("Escolha uma imagem ou um video para a criação do mapa de saliências:")
    cy.get('[style="text-align: center;"] > button').contains("Escolher Imagem")
    
    //Simulate loading image
    cy.get('input[type="file"]').attachFile('ambulancia.jpg')

    // Label and button to choose method
    cy.get('.centered-container > label').contains("Escolha um modelo para a criação do mapa de saliências:")
    cy.get('#casnet').select('CASNET 1')

    //Check containers
    cy.get('#imageContainer')
    cy.get('#emptyContainer')

    //Check button to create map
    cy.get('[style="text-align: center; margin-top: 20px;"] > button').contains("Criar mapa de saliências")
    cy.get('[style="text-align: center; margin-top: 20px;"] > button').click()

    //Check pop-up for map creation
    cy.get('.custom-dialog')
    cy.get('.custom-dialog > h2').contains("Aplicação para uso de Modelos de Atenção")
    cy.get('p').contains("Tem a certeza que pretende criar o mapa de saliências?")
    cy.get('.button-container > :nth-child(1)').contains("Criar mapa de saliências")
    cy.get('.button-container > :nth-child(2)').contains("Cancelar")

    cy.get('.button-container > :nth-child(2)').contains("Cancelar").click()
    
    //Check if loaded image is visible
    cy.get('#emptyContainer img').should('not.exist')
  })
})
  
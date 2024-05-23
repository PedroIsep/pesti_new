describe('template spec', () => {
  it('passes', () => {
    cy.visit('localhost:5173/login')
      
    cy.get('img')

    // Fill in the username and password fields
    cy.get('input[placeholder="Username"]').type('testuser')
    cy.get('input[placeholder="Password"]').type('testpassword123')
        
    // Submit the form
    cy.get('form').submit()
    
    // Logout button
    cy.get('a').contains("Logout")

    // Label and button to choose image
    cy.get('[style="text-align: center;"] > label').contains("Escolha uma imagem para a criação do mapa de saliências:")
    cy.get('[style="text-align: center;"] > button').contains("Escolher Imagem")
    
    //Simulate loading image
    cy.get('input[type="file"]').attachFile('ambulancia.jpg')

    //Check containers
    cy.get('#imageContainer')
    cy.get('#emptyContainer')

    //Check if loaded image is visible
    cy.get('#imageContainer img').should('be.visible')
  })
})
  
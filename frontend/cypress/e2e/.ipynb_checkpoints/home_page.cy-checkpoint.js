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
   
    // Label and button to choose method
    cy.get('.centered-container > label').contains("Escolha um modelo para a criação do mapa de saliências:")
    cy.get('#casnet').contains("Selecione um modelo...")
    cy.get('#casnet').contains("CASNET 1")
    cy.get('#casnet').contains("CASNET 2")
    
    //Check containers
    cy.get('#imageContainer')
    cy.get('#emptyContainer')

    //Check button to create map
    cy.get('[style="text-align: center; margin-top: 20px;"] > button').contains("Criar mapa de saliências")
    
    // Check line
    cy.get('[style="border-bottom: 4px solid black; margin: 20px auto; width: 90%;"]')

    //Check labels for notes
    cy.get(':nth-child(12) > h2').contains("Notas")
    cy.get(':nth-child(13)').contains("Criar uma Nota")

    //CHeck form to insert note
    cy.get('form')
    cy.get('form > label').contains("Conteudo:")
    cy.get('#content')

    //Button to submit note
    cy.get('form > input')

  })
})
  
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


  })
})
  
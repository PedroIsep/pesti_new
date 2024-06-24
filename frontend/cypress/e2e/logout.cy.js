describe('template spec', () => {
  it('passes', () => {
    cy.visit('https://9f9683d8-14d0-4581-b2f7-393d1ea2e5b2.e1-eu-north-azure.choreoapps.dev/login')
      
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
  
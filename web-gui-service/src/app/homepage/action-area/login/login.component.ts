import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';

import { ApplicativeUser } from '../../user';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.sass']
})
export class LoginComponent implements OnInit {

  constructor(private loggerService: LoggerService) { }

  ngOnInit(): void {
  }

  public submit(firstName: string, lastName: string, email: string): void {
    let userToSubmit = new ApplicativeUser();
    
    try {
      userToSubmit.setFirstName(firstName);
      userToSubmit.setLastName(lastName);
      userToSubmit.setEmail(email);
    }
    catch (err) {
      let errMsg = `Failed to update ApplicativeUser object details.\n${err}`;
      this.loggerService.error(LoginComponent.name, "submit", errMsg);
      return;
    }
  }

}

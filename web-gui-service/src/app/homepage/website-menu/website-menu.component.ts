import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';
import { Logo } from 'src/app/logo';
import { LogoService } from 'src/app/logo.service';

import { WebsiteMenuStateService } from './state.service';

@Component({
  selector: 'app-homepage-website-menu',
  templateUrl: './website-menu.component.html',
  styleUrls: ['./website-menu.component.sass']
})
export class WebsiteMenuComponent implements OnInit {

  public guestMode: boolean;
  public logo: Logo;

  constructor(
    private loggerService: LoggerService,
    private logoService: LogoService,
    private websiteMenuService: WebsiteMenuStateService
    ) {
      this.logo = new Logo();
      this.guestMode = true;
  }

  ngOnInit(): void {
    this.logoService.getLogo().subscribe({
      next: val => this.nextLogo(val),
      error: err => this.logoServiceError(err)
    });
  }

  public login(): void {
    this.websiteMenuService.loginState();
  }

  public logout(): void {
    this.websiteMenuService.initialState();
  }

  public signup(): void {
    this.websiteMenuService.signupState();
  }

  private logoServiceError(err: Error): void {
    let errMsg = `logoService has failed.\n${err}`;
    this.loggerService.error(WebsiteMenuComponent.name, "logoServiceError", errMsg);
  }

  private nextLogo(val: Logo): void {
    this.logo = val;
  }

}

import { Directive, ElementRef } from '@angular/core';

@Directive({
  selector: '[appLoginRequestErrorContainer]'
})
export class LoginRequestErrorContainerDirective {

  constructor(private el: ElementRef) { }

  public hide(): void {
    this.el.nativeElement.style.visible = false;
  }

  public show(): void {
    this.el.nativeElement.style.visible = true;
  }

}

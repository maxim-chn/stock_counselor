import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActionAreaComponent } from './action-area.component';

describe('ActionAreaComponent', () => {
  let component: ActionAreaComponent;
  let fixture: ComponentFixture<ActionAreaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ActionAreaComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ActionAreaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

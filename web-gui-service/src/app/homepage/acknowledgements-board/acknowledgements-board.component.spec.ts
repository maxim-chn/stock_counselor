import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AcknowledgementsBoardComponent } from './acknowledgements-board.component';

describe('AcknowledgementsBoardComponent', () => {
  let component: AcknowledgementsBoardComponent;
  let fixture: ComponentFixture<AcknowledgementsBoardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AcknowledgementsBoardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AcknowledgementsBoardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

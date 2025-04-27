import {Component, EventEmitter, Input, Output, SimpleChanges} from '@angular/core';
import {Card} from '../models/card';
import {NgForOf, NgIf} from '@angular/common';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import {HttpService} from '../services/http.service';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [
    NgIf,
    NgForOf,
    ReactiveFormsModule,
    FormsModule
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.css'
})
export class CardComponent {
  @Input() card: Card | undefined;
  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();
  @Output() refresh: EventEmitter<void> = new EventEmitter<void>();

  cardForm: FormGroup;

  constructor(private httpService: HttpService, private fb: FormBuilder) {
    this.cardForm = this.fb.group({
      title: [''],
      description: [''],
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['card'] && this.card) {
      this.cardForm.patchValue({
        title: this.card.title,
        description: this.card.description,
      });
    }
  }

  onSubmit(): void {
    if (this.card && this.card.idCard) {
      this.httpService.putCard(
        this.cardForm.value.description,
        this.card.idList,
        this.cardForm.value.title,
        this.card.idCard
      ).subscribe(
        (response: any): void => {
        this.close();
        this.refresh.emit();
      }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  deleteCard(): void {
    if (this.card && this.card.idCard) {
      this.httpService.deleteCard(this.card.idCard).subscribe(
        (response: any): void => {
          this.close();
          this.refresh.emit();
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  close(): void {
    this.closeModal.emit();
  }

  iaDescription: string = "";

  summarizeContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.card) {
      this.httpService.summarizeContent(this.cardForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  expandContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.card) {
      this.httpService.expandContent(this.cardForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  rewriteAndCorrectContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.card) {
      this.httpService.rewriteAndCorrectContent(this.cardForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  generateVariations(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.card) {
      this.httpService.generateVariations(this.cardForm.value.description).subscribe(
        (response: string[]): void => {
          let text: string = ""
          let n: number = 1;
          response.forEach((e: string): void => {
            text += "Alternativa " + n + ":\n" + e + "\n\n";
            n += 1;
          })
          this.iaDescription = text;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  correctContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.card) {
      this.httpService.correctContent(this.cardForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }
}

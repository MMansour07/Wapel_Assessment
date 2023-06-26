using EMS.Core.Dtos.Media;
using System;
using System.Collections.Generic;


namespace EMS.Core.Dtos.Evaluation
{
    public class EditEvaluationDto
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public double Salary { get; set; }
        public string Experience { get; set; }
        public int Vacancies { get; set; }
        public string UserId { get; set; }
        public List<MediaDto> Medias { get; set; }
        public DateTime CreatedDate { get; set; }
    }
}
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Web;


namespace EMS.Core.Dtos.Evaluation
{
    public class EditEvaluationPostDto
    {
        public int Id { get; set; }

        [Required(ErrorMessage = "Required Field")]
        public string Title { get; set; }
        [Required(ErrorMessage = "Required Field")]
        public string Description { get; set; }
        [Required(ErrorMessage = "Required Field")]
        public double Salary { get; set; }
        [Required(ErrorMessage = "Required Field")]
        public string Experience { get; set; }
        [Required(ErrorMessage = "Required Field")]
        public int Vacancies { get; set; }
        public string UserId { get; set; }
        public List<int> EliminatedIds { get; set; }
        public List<string> PublicIds { get; set; }
        public DateTime CreatedDate { get; set; }
        public List<HttpPostedFileBase> NewFiles { get; set; }
        public List<string> Titles { get; set; }

        //public List<EMS.Core.Model.Media> ToMedialst(EditJobPostDto src, List<EMS.Core.Model.Media> dest)
        //{
        //    int x = src.Titles.Count - dest.Count;
        //    foreach (var item in dest)
        //    {
        //        item.Title = src.Titles[x];
        //        item.JobId = src.Id;
        //        x++;
        //    }
        //    return dest;
        //}
    }
}
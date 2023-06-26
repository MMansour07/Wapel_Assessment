using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Web;


namespace EMS.Core.Dtos.Evaluation
{
    public class NewEvaluationDto
    {
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
        public List<HttpPostedFileBase> Files { get; set; }
        public List<string> Titles { get; set; }

        //public EMS.Core.Model.Department ToJob(NewJobDto src, EMS.Core.Model.Department dest, ICollection<EMS.Core.Model.Media> lst)
        //{
        //    dest.Medias = lst;
        //    int x = 0;
        //    // worest case scenario iterate 3 times
        //    foreach (var item in dest.Medias)
        //    {
        //        item.Title = src.Titles[x];
        //        x++;
        //    }

        //    return dest;
        //}
    }
}
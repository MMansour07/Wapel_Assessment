

using System;

namespace EMS.Core.Model
{
    public class Evaluation : BaseEntity
    {
        public float WorkQuality { get; set; }
        public float RelationshipWithCoworkers { get; set; }
        public float Initiative { get; set; }
        public float Communication { get; set; }
        public float Attitude { get; set; }
        public string Comments { get; set; }
        public DateTime? EvaluationDate { get; set; }
    }
}

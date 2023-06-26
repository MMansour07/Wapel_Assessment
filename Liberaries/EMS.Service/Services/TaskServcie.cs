using AutoMapper;
using EMS.Core.Dtos.General;
using EMS.Core.Interfaces;
using EMS.Service.Interfaces;
using System;
using System.Threading.Tasks;
using EMS.Core.Dtos.Task;
using System.Collections.Generic;
using System.Data.Entity;

namespace EMS.Service.Services
{
    public class TaskServcie : ITaskServcie
    {
        private readonly IRepository<Core.Model.Task> _taskRepo;
        private IMapper _autoMapper;
        public TaskServcie(IMapper autoMapper, IRepository<Core.Model.Task> taskRepo)
        {
            _autoMapper = autoMapper;
            _taskRepo = taskRepo;
        }

        public async Task<ResponseModel<NewTaskDto>> CreateTaskAsync(NewTaskDto obj)
        {
            try
            {
                var taskCriteria =  await _taskRepo.Add(_autoMapper.Map<NewTaskDto, Core.Model.Task>(obj));

                return new ResponseModel<NewTaskDto>()
                {
                    Success = true,
                    Data = _autoMapper.Map<Core.Model.Task, NewTaskDto>(taskCriteria)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<NewTaskDto>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<List<TaskDto>>> GetTasksByCriteriaId(int TaskCriteriaId)
        {
            try
            {
                var result = await _taskRepo.Filter( i => i.TaskCriteriaId == TaskCriteriaId).ToListAsync();

                return new ResponseModel<List<TaskDto>>()
                {
                    Success = true,
                    Data = _autoMapper.Map<List<Core.Model.Task>, List<TaskDto>>(result)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<List<TaskDto>>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
    }
}
